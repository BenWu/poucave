import asyncio

from kinto_http import Client


def get_timestamp(client, bucket, collection):
    return client.get_records_timestamp(bucket=bucket, collection=collection)


# TODO: should retry requests. cf. lambdas code
async def run(request, server):
    """Make sure that entries in monitoring endpoint have the timestamps as
    their records endpoint.
    """
    loop = asyncio.get_event_loop()

    client = Client(server_url=server, bucket="monitor", collection="changes")
    entries = client.get_records()
    futures = [
        loop.run_in_executor(
            None, get_timestamp, client, entry["bucket"], entry["collection"]
        )
        for entry in entries
    ]
    results = await asyncio.gather(*futures)
    data = {}
    for (entry, timestamp) in zip(entries, results):
        cid = "{bucket}/{collection}".format(**entry)
        data[cid] = str(timestamp) == str(entry["last_modified"])

    return all(data.values()), data
