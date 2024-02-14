# Plant Parent🪴

Find plants that are right for your lifestyle and get helpful tips to keep them alive!

## Features

### A logged-out user can:

- Browse plants by an alphabetized list
- Search for a specific plant
- Select filters based on various parameters such as ‘indoor plant’ or ‘sunlight preferences’, and ‘edible’.
  - This allows users to get more refined and specific results based on their situation and needs.
- Signup for an account

### A logged-in user can:

- Do everything a logged-out user can
- Apply preference filters such as indoor or edible which will be automatically applied when they search and suggested plants on homepage will adhere to user preferences
- Save plants to a favorites list
  - If a user finds an interesting plant or a plant they are caring for and wants to easily access the care plan, this would be helpful
- Update/delete their profile
  - A user’s personal information and/or preferences may change so it’s convenient for a user to update their profile.

## User Flow

For both a logged-in and logged-out user, the homepage shows a search bar where a user can search for a plant. There will be a link to a page of plants listed in alphabetical order where a user can browse. If a user is logged in they’ll be able to see recommended plants under the search bar which will be randomly selected plants. If the user has saved preferences, they will see plants that are filtered based on their preferences. Under the search bar will be checkboxes to search for plants with preferences.

When a user searches for plants and receive results, they can click on a plant to view details and to see their care guide. If a user is logged in they’ll have the option to save the plant to their favorites. If they are not logged in, they will be redirected to a registration page.

In the navbar for a logged-out user, they will see a homepage link, a search plants link, and a view all plants link. A logged-in user will also see a navbar link of their favorites and another navbar link of their username which they can click on which will take them to a page that includes the following options- edit profile and log out.

## API

Plant Parent is run by the [Perenual](https://perenual.com/docs/api) API.

## Tech Stack

- Frontend: HTML, CSS, JavaScript, styled with Bootstrap. Theme is ‘minty’ from bootswatch
- Backend: Python, Flask, SQLAlchemy, PostgreSQL, WTForms

### Important Note

Plant Parent can only handle 100 API calls per day, as detailed by the Perenual API free plan. If no results are being returned Plant Parent has exceeded the daily limit of API calls. If that's the case, please try searching for plants the next day!
