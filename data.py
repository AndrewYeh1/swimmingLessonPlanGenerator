import activityTemplates

ACTIVITIES = {
    "Flutter kick": {
        "basic": activityTemplates.Template("Flutter kick", 5, [1, 2], 1),
        "second": activityTemplates.Template("Flutter kick", 10, [1], 2),
        "third": activityTemplates.Template("Flutter kick", 7, [1], 3),
        "fourth": activityTemplates.Template("Flutter kick", 10, [3], 2)
    }
}
