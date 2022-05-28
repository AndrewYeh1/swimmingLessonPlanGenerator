from templates import activityTemplates

intro = activityTemplates.Template("Intro", 5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0)

ACTIVITIES = {
    "Flutter kick": [
        activityTemplates.Template("One", "Flutter kick", 5, [1, 2], 1),
        activityTemplates.Template("Two", "Flutter kick", 10, [1], 2),
        activityTemplates.Template("Three", "Flutter kick", 7, [1], 3),
        activityTemplates.Template("Four", "Flutter kick", 10, [3], 2)
    ]
}
