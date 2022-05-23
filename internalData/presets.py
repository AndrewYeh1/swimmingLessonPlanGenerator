from templates import activityTemplates

options = {
    "Intro": {
        "intro": activityTemplates.Template("Other", 5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, ["Introduce myself"]),
        "introDefault": True
    },
    "Others": {
        "defaultLevel": "Swim kids 1"
    }
}
