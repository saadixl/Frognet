## Why the name Frognet though?
If you search for a the phrase "Eat that frog" then Google will return you the following text: "Eating the frog is the process of identifying your most difficult task of the day and completing it before you do any other work". I just wanted to build a tool which can catch the frogs for me.

## How it works?
- The Python/Flask microservices are running in a VPC
- The webhook code is running using a serverless function (so that I can use HTTPS and standard end-points without ports enforced by Todoist)

## Demo
Right now adding a new item triggers the automatic prioritization. It's very very slow. Next target is to improve the performance.

<img width="535" alt="Screenshot 2024-01-27 at 8 32 42 PM" src="https://github.com/saadixl/Frognet/assets/1633940/462ac549-25f8-4b68-a8d1-9c7ce95e9688">
