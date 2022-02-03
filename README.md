# Heatmap (Comet Circle)

A Streamlit app to see a heatmap of all sections of classes at UTD and filter by relevant majors or schools. This was primarily intended for event organizers to see the best time to schedule their events, but can used by just about anyone.

Access on http://heatmap.utdnebula.com/:

## Background

This project was originally made for [HackUTD-2021F](https://devpost.com/software/comet-clique), but because the project was so _amazing_, Project nebula decided to pick it and maintain it!

### Local Installation process

1. clone the repo locally
2. Create an Anaconda environment for the project (Download [Anaconda](https://www.anaconda.com/products/individual) if not installed already)
3. Open the environment with the terminal and go into the project directory (use cd for windows)
4. run the command: pip install -r requirements.txt
5. run the command: streamlit run main.py

it should be running in your browser now, create an issue if you're having trouble!

### Deployment on Google Cloud Run

This section is meant for maintainers only

1. Make sure you have [google cloud CLI](https://cloud.google.com/sdk/docs/install) installed

2. make sure you are signed in google cloud cli and also have a project for your account

3. Go to the project directory in the console

4. Run the command, replacing \<ProjectName> and \<AppName> accordingly (AppName could be anything, but Project Name must be the project already made in Google Cloud):

```
gcloud builds submit --tag gcr.io/<ProjectName>/<AppName>  --project=<ProjectName>
```

5. Then run the command with the same variables from step 4

```
gcloud run deploy --image gcr.io/<ProjectName>/<AppName> --platform managed  --project=<ProjectName> --allow-unauthenticated
```

6. you will be prompted multiple times during all of this
    - if it asks to install API's, say yes
    - when it prompts you for service name, return to skip
    - when it prompts you to specify region, use 23 (us-central1)

It should give you a url where your project is being hosted. contact @TrystonMinsquero if you're having any trouble!
