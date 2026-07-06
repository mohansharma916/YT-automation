from datetime import datetime
import time

import gspread
from google.oauth2.service_account import Credentials

from app.models.sheet_job import SheetJob


class GoogleSheetService:

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    MAX_RETRIES = 3

    def __init__(self):

        credentials = Credentials.from_service_account_file(
            "app/config/credentials.json",
            scopes=self.SCOPES,
        )

        self.client = gspread.authorize(
            credentials,
        )

        self._cache = {}

    ####################################################
    # Sheet
    ####################################################

    def sheet(
        self,
        sheet_name: str,
    ):

        if sheet_name not in self._cache:

            self._cache[sheet_name] = (
                self.client
                .open(sheet_name)
                .sheet1
            )

        return self._cache[sheet_name]

    ####################################################
    # Retry
    ####################################################

    def _retry(
        self,
        func,
    ):

        last_error = None

        for attempt in range(self.MAX_RETRIES):

            try:

                return func()

            except Exception as ex:

                last_error = ex

                print(
                    f"Google Sheet Retry {attempt + 1}/{self.MAX_RETRIES}"
                )

                time.sleep(2)

        raise last_error

    ####################################################
    # Read Pending Job
    ####################################################

    def get_pending_job(
        self,
        sheet_name: str,
    ) -> SheetJob | None:

        sheet = self.sheet(
            sheet_name,
        )

        rows = self._retry(
            lambda: sheet.get_all_values()
        )

        for index, row in enumerate(
            rows[1:],
            start=2,
        ):

            while len(row) < 8:
                row.append("")

            status = row[2].strip().upper()

            if status not in ("", "PENDING"):
                continue

            return SheetJob(
                row=index,
                job_id=row[0].strip(),
                audio_url=row[1].strip(),
                status=status,
            )

        return None

    ####################################################
    # Generic Update
    ####################################################

    def update(
        self,
        sheet_name: str,
        cell: str,
        value: str,
    ):

        sheet = self.sheet(
            sheet_name,
        )

        self._retry(
            lambda: sheet.update(
                cell,
                [[value]],
            )
        )

    ####################################################
    # Timestamp
    ####################################################

    def update_timestamp(
        self,
        sheet_name: str,
        row: int,
    ):

        self.update(
            sheet_name,
            f"H{row}",
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),
        )

    ####################################################
    # Status
    ####################################################

    def update_status(
        self,
        sheet_name: str,
        row: int,
        status: str,
    ):

        self.update(
            sheet_name,
            f"C{row}",
            status,
        )

        self.update_timestamp(
            sheet_name,
            row,
        )

    ####################################################
    # Uploaded URL
    ####################################################

    def update_uploaded_url(
        self,
        sheet_name: str,
        row: int,
        url: str,
    ):

        self.update(
            sheet_name,
            f"D{row}",
            url,
        )

    ####################################################
    # Title
    ####################################################

    def update_title(
        self,
        sheet_name: str,
        row: int,
        title: str,
    ):

        self.update(
            sheet_name,
            f"E{row}",
            title,
        )

    ####################################################
    # Description
    ####################################################

    def update_description(
        self,
        sheet_name: str,
        row: int,
        description: str,
    ):

        self.update(
            sheet_name,
            f"F{row}",
            description,
        )

    ####################################################
    # Error
    ####################################################

    def update_error(
        self,
        sheet_name: str,
        row: int,
        error: str,
    ):

        self.update(
            sheet_name,
            f"G{row}",
            error,
        )

        self.update_timestamp(
            sheet_name,
            row,
        )