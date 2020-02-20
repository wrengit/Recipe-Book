# Recipe Book

Milestone 3 project: Data-centric Development - Code Institute

An online recipe book where users can find, upload, edit and delete recipes. Backend made with python & flask.

![App on multiple screens](multiscreen.jpg)

## Demo

A link to the project hosted on Heroku can be found [here](https://wrengit-milestone3.herokuapp.com)

## UX

The UX was designed to be as clean and clutter free as possible. From experience, often when a user is searching for a recipe online, sites were found to contain too much information, and made finding the ingredients list or method cumbersome. The Material design philosophy was followed, drawing inspiration from the card and paper styles. 

The colour scheme was obtained from the Material.io colour-picker tool, using two complimentary, but contrasting colours. 

When a user selects a recipe, they are not navigated away from the main page. Instead a large modal contains all required information. Recipe cards show a title, large image, short recipe descirption and tags to indicate the type of recipe.

A fixed navigation bar was chosen to ensure that users always had access to the tags filtering, to quickly locate a recipe that meets their needs. Recipes can also be searched over by ingredient(s), which also allow tag filtering. 

## DB Schema

MongoDB Atlas was chosen as the DB to allow change to be made the the DB schema in future, if upgrading or changing the site. The server is cloud based to ensure continuous uptime, and to allow the recipes to persist on Heroku, which periodically restarts their servers, removing any locally stored content. 

There are two collection in the DB. These are the 'users' collection and the 'recipes' collection. 

Schemas for the two collections can be found below.

`users`

``` 
{user
        {_id: unique objectId}
        {name: username},
        {email: user@email.com},
        {password: hashed password},
        {is_admin: Boolean}
    }
```

`recipes`

```
{recipes
        {_id: unique objectId}
        {name: recipe name},
        {desc: recipe description},
        {ingredients [
            {ingredient string field},
            {ingredient string field},
            { ... }
            ]},
        {method: recipe method},
        {owner: recipe owner (username)},
        {tags [
            {tag},
            {tag}, 
            {tag}
        ]},
        {image: url to image location},
        {likes: [
            {username},
            {username},
            {username}
        ]}
```


## Features

### Existing Features

- Full text search of recipe ingredients

   Sumbitting the search field will search the DB recipes ingredients field for all matching words. Common words, such as 'and', 'of', etc are ommited from the search and will not return any results

- Filtering of recipes based on a selection of 'tags'

   The user is presented with 6 'tags' when posting a recipe. These allow filtering of the recipes to narrow down recipes that other users may or may not be interested in

- Favouriting, or liking a recipe to save to profile page for future reference

   This serves to show the popularity of a recipe to help users decide, as a form of peer review. This feature also gives content creators feedback on their content, inspiring them to post more
   
- Adding, editing and deleting of user recipes

   Users have full control over their recipes, with only the user able to edit or delete their own recipes

### Features Left to Implement

- Upgrade ingredient text search to rank results based on matching ingredients. Currently the search will return all recipes that contain the search field. If a user searches for two ingredients (a + b), and recipe 1 contains a, whilst recipe 2 contains a + b, then the results should display recipe 2 first
- Add abilty to sort recipes by 'like' rating
- Add abilty to change user password, and potentially email user if password has been forgot


## Technologies Used

- Python
- Flask
- MongoDB
- PyMongo
- Flask-wtf
- Flask-login
- Gunicorn
- HTML
- CSS
- Bootstrap - Material Design by fezvrasta (https://fezvrasta.github.io/bootstrap-material-design/)
- Bootstrap
- Material Icons
- Font Awesome
- Google Fonts
- JavaScript
- PopperJS
- jQuery

## Services Used

- Tinypng - image compression
- Unsplash - image repository
- favicon.io - favicon & logo generator
- Material.io - Material design colour picker

## Testing

The site was developed on a Dell XPS 13 13" 2-in-1 touch screen laptop. Initial testing was conducted with Brave Browser, Microsoft Edge, and Chrome. Mobile testing used a Huawei P20 pro, using Brave, Chrome, and Firefox. There was no availability of Apple devices, either mobile or desktop to conduct testing.

All testing was conducted manually.

The site was tested with W3 html & css validators.
Accessabilty was checked with https://wave.webaim.org/.

### Browser compatibility

The app displays as expected on all browsers tested. 

### User stories

> As a user I want to be able to quickly and easily search for a recipe based on specified criteria (ingredients, vegetarian, etc)
>
> > The user can search for recipes based on included ingredients, and/or filter recipes by a series of tags to narrow down the right recipe. This is easily done, with the search and tags section prominently displayed at the top of the page, or in the navbar toggle menu on mobiles

> As a user I would like to be able to save or like recipes, so I can revisit them quickly next time I visit the site
>
> > The user may open a recipe, and if logged in, can like or favourite the recipe. The list of liked recipes can be found in the profile section for a user to quickly locate on return to the page

> As a user I want to post and share my own recipes for others to use. Getting 'likes' on my recipes would encourage me to post more
>
> > The user can post a recipe, once logged in, and the abilty to do so is clearly shown on the jumbotron on the index/home page. Users can see how many likes their recipe has recieved, which ensures that they contribute further to the site, and gives sense that other users are enjoying their content

> As a user I want to delete or edit my posted recipes, if I no longer wish them to be online, or have decided to change the method or ingredients
>
> > The user is able to easily edit or delete a recipe that they own, from within the recipe modal. This information is presented clearly at the bottom of the modal. Editing a recipe is easy, with the form prepopulated with the exisiting recipe information. To delete a recipe, the site will ask the user to confirm that they want to delete the recipe. This is to ensure a misplaced click does not delete content unneccasarily.

## Cloning & Deployment

### Cloning

The site can be cloned to a local repository by the following steps (GitHub guide link [here](https://help.github.com/en/articles/cloning-a-repository)):

- Under the repository name, click Clone or download.

- In the Clone with HTTPs section, click the clipboard icon to copy the clone URL for the repository.

- Open the terminal on your local machine

- Change the current working directory to the location where you want the cloned directory to be made.

- Type `git clone`, and then paste the URL you previously copied.

\$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY

- Press Enter. Your local clone will be created.

```

> Cloning into `Spoon-Knife`...
> remote: Counting objects: 10, done.
> remote: Compressing objects: 100% (8/8), done.
> remove: Total 10 (delta 1), reused 10 (delta 1)
> Unpacking objects: 100% (10/10), done.

```

### Deployment

The site is deployed on Heroku, on the free tier. This has limited dynos and is intended to simply show the site functioning. This free tier is not for production ready use. 

The site is deployed by linking the main GitHub repository master branch to Heroku. The environment variables are entered on the app settings. These include the MONGO_URI, and flask SECRET_KEY.

## Credits

### Content

All code is written by me (wrenna). Recipes and user content are by me, friends, family and other users.

### Media

Recipe images (by wrenna) are from [Unsplash](http://unsplash.com), a royalty free, free to use image repository. Photographer credits for the images are below. Users have the abilty to link to web images.

