import os

class Compile():
    def __init__(self, config, init, preload, create, update):
        self.config = config
        self.init = init
        self.preload = preload
        self.create = create
        self.update = update
        self.name = self.config["name"]
        self.final = ""

    def compile(self):
        first_parts = """<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <style>
        body{
            margin: 0;
            padding: 0;
            background: #121920;
        }
    </style>
    <title>""" + self.name + """</title>
</head>
<body>
<script>\n\n"""

        path = os.path.join(os.getcwd(), "static")
        path = os.path.join(path, "js")
        path = os.path.join(path, "engine.js")
        with open(path, "r") as f:
            engine = f.read()
        
        helper_path = os.path.join(os.getcwd(), "static")
        helper_path = os.path.join(helper_path, "lib")
        helper_path = os.path.join(helper_path, "EGB-Helper.js")
        with open(helper_path, "r") as f:
            helper = f.read()

        first_parts += str(engine)
        first_parts += "\n\n\n"
        
        first_parts += str(helper)
        first_parts += "\n\n\n"

        last_parts = """\n</script>
</body>
</html>"""

        config = "var False = false;\n \
            var config = {\ntype: Phaser.AUTO, width: " + str(self.config["width"]) + \
            ", height: " + str(self.config["height"]) + ", "
        
        if "else" in self.config:
            for i in self.config["else"].keys():
                if self.config["else"][i] == False:
                    self.config["else"][i] = "false"
                config += str(i) + ": " + str(self.config["else"][i]) + ", "
        else:
            pass

        config_last = "scene: { preload: preload, create: create, update: update }\n}\n"
        config += config_last

        first_parts += "\n" + str(self.init) + "\n"

        first_parts += config

        first_parts += "\nvar game = new Phaser.Game(config);"
        
        first_parts += "\nfunction preload(){\n" + self.preload + "\n}"
        first_parts += "\nfunction create(){\n" + self.create + "\n}"
        first_parts += "\nfunction update(){\n" + self.update + "\n}"
        
        first_parts += last_parts

        return first_parts