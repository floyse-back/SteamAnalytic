from typing import List

from app.domain.steam.sync_repository import ICalendarSteamEventRepository
from bs4 import BeautifulSoup
import requests
from datetime import date

from app.infrastructure.celery_app.celery_app import logger


class UpdateCalendarEventsUseCase:
    MONTHS_FULL = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    MONTHS_SHORT= {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }

    def __init__(self,calendar_repository:ICalendarSteamEventRepository):
        self.calendar_repository = calendar_repository
        self.url_steamworks = "https://partner.steamgames.com/doc/marketing/upcoming_events?language=english"


    def execute(self,session):
        data = self.__parse_steamworks()
        self.calendar_repository.update_calendar_data(session=session,data=data)
        logger.info(f"Steam Events Updated")


    @classmethod
    def __correct_date(cls,date_text:str,full_month:bool=False):
        splited_data = date_text.split(" ")
        logger.debug(f"Splited data: %s",splited_data)
        logger.debug(f"Month: %s",splited_data[0])
        logger.debug(f"MONTHS_FULL: %s",cls.MONTHS_FULL)
        if full_month:
            type_month = cls.MONTHS_FULL[f'{splited_data[0]}']
        else:
            type_month = cls.MONTHS_SHORT.get(splited_data[0])
        logger.debug(f"Type_month: %s",type_month)
        if type_month is None:
            logger.error(f"Invalid month: %s",date_text)
            raise Exception("Invalid month")
        if len(splited_data) == 2:
            year = date.today().year
            day = splited_data[1]
        else:
            year = splited_data[2]
            day = splited_data[1]
        return date(year=int(year),month=type_month,day=int(day))


    def __correct_steamworks_event_sale(self,text,full_month:bool=True):
        """
        Перетворює текст на name,date_start,date_end
        """
        data_list:List[str] = text.split("|")
        logger.debug(f"data_list: %s",data_list)
        dates_text = data_list[1].replace(",","").split("-")
        logger.debug(f"dates_text: %s",dates_text)
        name = data_list[0].strip()
        date_start = self.__correct_date(dates_text[0].strip(),full_month=full_month)
        date_end = self.__correct_date(dates_text[1].strip(),full_month=full_month)
        return name,date_start,date_end,"sale"

    def __corrected_date_from_festival(self,dates_text):
        dates_text = str(dates_text).strip()[4:-5]
        date_split = dates_text.split("<br/>")
        date_start = self.__correct_date(date_split[0].strip())
        date_end = self.__correct_date(date_split[1].strip())

        return date_start,date_end


    def __parse_steamworks(self):
        response = requests.get(self.url_steamworks)
        if response.status_code != 200:
            return False
        soup = BeautifulSoup(response.text, "html.parser")
        h2_bb_subsection = soup.find_all(class_="bb_subsection")

        if h2_bb_subsection is None:
            logger.critical(f"Steam Website does not contain a bb_subsection")
            return None

        logger.debug("%s",h2_bb_subsection)
        answer_data = []
        for line in h2_bb_subsection:
            try:
                answer_data.append(self.__correct_steamworks_event_sale(line.text.strip(),full_month=True))
            except Exception as e:
                logger.error(f"Error:%s\n line %s",e,line,exc_info=True)
        festival_data = soup.find(class_="documentation_bbcode").find("table").find_all("tr")[1:-1]
        if festival_data is None:
            logger.critical(f"Steam Website does not contain a bb_subsection")
            return None
        for event in festival_data:
            try:
                td_event = event.find_all("td")
                if td_event[2].text != "-":
                    name = td_event[1].text.strip()
                    date_start,date_end = self.__corrected_date_from_festival(td_event[0])
                    answer_data.append((name,date_start,date_end,"festival"))
            except Exception as e:
                logger.error(f"Error:%s\n line %s",e,event,exc_info=True)

        return answer_data