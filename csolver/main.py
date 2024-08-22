from typing import Optional, Literal, Union
from urllib.parse import urlparse, parse_qs
import time
import os
import re

import requests

from .exceptions import (
    BadRequest,
    TaskProcessing,
    TaskFailed,
    TaskCompleted,
    NoBalance,
    NoToken
)

BASE: str = "https://api.csolver.xyz/"

class Solver:
    def __init__(self, api_key: Optional[str] = None, job_sleep: Optional[Union[int, float]] = 3.5) -> None:
        self.api_key: str = api_key or os.environ.get("api_key")
        self.job_sleep: Union[int, float] = job_sleep

        self.session: requests.Session = requests.Session()
        self.session.headers.update({
            "API-Key": self.api_key
        })
        
    def get_balance(self) -> float:
        resp = self.session.post(
            BASE + "getbal",
            json={"api_key": self.api_key}
        )

        if not resp.ok:
            raise BadRequest()
        
        if (balance := resp.json().get("bal")) == 0:
            raise NoBalance()

        return balance
        
    def fetch_result(self, job: Union[str, int]) -> Optional[str]:
        while True:
            resp = self.session.get(
                BASE + f"result/{job}"
            )

            if not resp.ok:
                raise TaskFailed()
            
            data = resp.json()
            status: str = data.get("status")

            if status == "completed":
                return data["solution"]

            elif status == "processing":
                time.sleep(self.job_sleep) 

            elif status == "Failed":
                raise TaskFailed()

    def solve_hcap(
        self,
        task: Literal["hCaptcha", "hCaptchaEnterprise"],
        site_key: str,
        site: str,
        proxy: Optional[str] = None,
        rqdata: Optional[str] = None
    ) -> Optional[str]:
        assert self.api_key, "API key must be provided"

        resp = self.session.post(
            BASE + "solve",
            json={
                "task": task,
                "sitekey": site_key,
                "site": site,
                "proxy": proxy,
                "rqdata": rqdata
            }
        )

        resp.raise_for_status()

        data = resp.json()
        job_id: Union[str, int] = data.get("job_id")

        if job_id:
            return self.fetch_result(job_id)

        raise TaskFailed()
    
    def solve_recap(
        self, 
        invisible: bool, 
        anchor: str, 
        reload: str
    ) -> str:
        headers: dict = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
        }

        resp = requests.get(anchor, headers=headers)
        resp.raise_for_status()

        token_match = re.search(r'type="hidden" id="recaptcha-token" value="([^"]+)"', resp.text)
        
        if not token_match:
            raise NoToken()
            
        token: str = token_match.group(1)
        uv: dict = parse_qs(urlparse(anchor).query)

        v, k, co = uv["v"][0], uv["k"][0], uv["co"][0]

        data: str = f"v={v}&reason=q&c={token}&k={k}&co={co}&hl=en&size={'invisible' if invisible else 'visible'}"

        headers.update({
            "Referer": resp.url,
            "Content-Type": "application/x-www-form-urlencoded"
        })

        resp = requests.post(
            reload, 
            headers=headers, 
            data=data
        )
        resp.raise_for_status()

        return resp.text.split('["rresp","')[1].split('"')[0]
