from cassiopeia import Queue

RANKED_QUEUE_IDS = {
    "solo": Queue.ranked_solo_fives,
    "flex": Queue.ranked_flex_fives
}

QUEUE_ANNOTATES = {
    Queue.blind_fives: "5v5 Blind",
    Queue.normal_draft_fives: "5v5 Normal Draft",
    Queue.ranked_solo_fives: "5v5 Ranked Solo",
    Queue.ranked_flex_fives: "5v5 Ranked Flex",
    Queue.clash: "5v5 Clash",
    Queue.aram: "ARAM"
}
