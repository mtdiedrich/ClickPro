import aws_cdk as core
import aws_cdk.assertions as assertions

from click_pro.click_pro_stack import ClickProStack

# example tests. To run these tests, uncomment this file along with the example
# resource in click_pro/click_pro_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ClickProStack(app, "click-pro")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
