from __future__ import annotations

import asyncio
import random
import time

from aiohttp import ClientSession


class VictoriaMetricsSession:
    async def send_metric(
        self,
        metric_name: str,
        metric_data: str,
        instance_name: str,
        job_name: str = "scraper",
    ):
        metric_format = (
            f"?format=1:time:unix_ms"
            f",2:metric:{metric_name}"
            f"&extra_label=instance={instance_name}"
            f"&extra_label=job={job_name}"
        )

        url = "http://localhost:8428/api/v1/import/csv" + metric_format

        async with self.session.post(url, data=metric_data) as resp:
            pass

    async def __aenter__(self) -> VictoriaMetricsSession:
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()


async def main():
    try:
        async with VictoriaMetricsSession() as session:
            while True:
                time_ms = int(time.time() * 1000)
                online = round(random.random())
                await session.send_metric(
                    metric_name="alias",
                    metric_data=f"{time_ms},{online}",
                    instance_name="tg",
                )
                time.sleep(2)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    asyncio.run(main())
