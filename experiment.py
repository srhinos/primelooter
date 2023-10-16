import httpx
import json
import asyncio
import re
import logging
import http.cookiejar as cookiejar

gql_url = "https://gaming.amazon.com/graphql"

logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger()
offers_payload = {
    "operationName": "OffersContext_Offers_And_Items",
    "variables": {"pageSize": 999},
    "extensions": {},
    "query": "query OffersContext_Offers_And_Items($dateOverride: Time, $pageSize: Int) {\n  inGameLoot: items(\n    collectionType: LOOT\n    dateOverride: $dateOverride\n    pageSize: $pageSize\n  ) {\n    items {\n      ...Item\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Item on Item {\n  id\n  isDirectEntitlement\n  requiresLinkBeforeClaim\n  grantsCode\n  isDeepLink\n  isFGWP\n  offers {\n    ...Item_Offer\n    __typename\n  }\n  game {\n    ...Game\n    __typename\n  }\n  __typename\n}\n\n\nfragment Item_Offer on Offer {\n  id\n  offerSelfConnection {\n    eligibility {\n      ...Item_Offer_Eligibility\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Item_Offer_Eligibility on OfferEligibility {\n  isClaimed\n  canClaim\n  missingRequiredAccountLink\n}\n\nfragment Game on GameV2 {\n  id\n  assets {\n    title\n    publisher\n  }\n}\n",
}


async def claim_offer(offer_id: str, item: dict, client: httpx.AsyncClient, headers: dict) -> True:
    if item["offers"][0]["offerSelfConnection"]["eligibility"]["isClaimed"] != True:
        if (
            item["offers"][0]["offerSelfConnection"]["eligibility"]["canClaim"] == False
            and item["offers"][0]["offerSelfConnection"]["eligibility"]["missingRequiredAccountLink"] == True
        ):
            log.error(f"Cannot collect game `{item['game']['assets']['title']}`, account link required.")
            return
        log.info(f"Collecting offer for {item['game']['assets']['title']}")
        claim_payload = {
            "operationName": "placeOrdersDetailPage",
            "variables": {
                "input": {
                    "offerIds": [offer_id],
                    "attributionChannel": '{"eventId":"ItemDetailRootPage:' + offer_id + '","page":"ItemDetailPage"}',
                }
            },
            "extensions": {},
            "query": "fragment Place_Orders_Payload_Order_Information on OfferOrderInformation {\n  catalogOfferId\n  claimCode\n  entitledAccountId\n  entitledAccountName\n  id\n  orderDate\n  orderState\n  __typename\n}\n\nmutation placeOrdersDetailPage($input: PlaceOrdersInput!) {\n  placeOrders(input: $input) {\n    error {\n      code\n      __typename\n    }\n    orderInformation {\n      ...Place_Orders_Payload_Order_Information\n      __typename\n    }\n    __typename\n  }\n}\n",
        }

        response = await client.post(gql_url, headers=headers, data=json.dumps(claim_payload))
        if response.json()["data"]["placeOrders"]["error"] != None:
            log.error(f"Error: {response.json()['data']['placeOrders']['error']}")


async def primelooter(cookie_file):
    jar = cookiejar.MozillaCookieJar(cookie_file)
    jar.load()
    async with httpx.AsyncClient() as client:
        base_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        }

        json_headers = base_headers | {
            "Content-Type": "application/json",
        }
        for _c in jar:
            client.cookies.jar.set_cookie(_c)

        html_body = (await client.get("https://gaming.amazon.com/home", headers=base_headers)).text
        matches = re.findall(r"name='csrf-key' value='(.*)'", html_body)
        json_headers["csrf-token"] = matches[0]

        response = await client.post(gql_url, headers=json_headers, data=json.dumps(offers_payload))
        data = response.json()["data"]["inGameLoot"]["items"]

        coros = await asyncio.gather(
            *[claim_offer(item["offers"][0]["id"], item, client, json_headers) for item in data]
        )
