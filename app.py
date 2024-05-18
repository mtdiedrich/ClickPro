#!/usr/bin/env python3
import os

import aws_cdk as cdk

from click_pro.click_pro_stack import ClickProStack


app = cdk.App()
ClickProStack(app, "ClickProStack")
app.synth()