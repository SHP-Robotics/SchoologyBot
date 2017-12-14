import asyncio

from schoology_client import SchoologyClient

client = SchoologyClient('../schoology_cred.json')


async def main():
    a = await client.post_update('725319913', "Another schoology API test.")
    print(a)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
