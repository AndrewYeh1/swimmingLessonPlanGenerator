from templates import activityTemplates

INTRO = activityTemplates.Template("Intro", 5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0)

ACTIVITIES = {
    "Flutter kick": {
        "basic": activityTemplates.Template("Flutter kick", 5, [1, 2], 1),
        "second": activityTemplates.Template("Flutter kick", 10, [1], 2),
        "third": activityTemplates.Template("Flutter kick", 7, [1], 3),
        "fourth": activityTemplates.Template("Flutter kick", 10, [3], 2)
    }
}
