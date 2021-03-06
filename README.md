# Quick Overview
This project is a source code that runs my <a href="https://arsenychebyshev.pythonanywhere.com/">DjangoPet</a> website.
<p>The functionality of the site covers most of the Backend Development necessities,
such as building a code architecture, connecting databases to the controllers,
filtering data, securing it for end-user interfaces, processing templates server-side,
building business-logic in detached modules. Currently, though, there is no general purpose for this site, it is just an overview of technologies I'm capable of using.</p>
<p>Currently few microservices (apps) are running:</p>
<ul>
  <li>Polls app : supports Object Relational Mapping to the database, generating pages with dynamic content and end-user POST form submitting </li>
  <li>Sessions app: supports giving cookies from server to client. Cookies might be sessional (i.e. expiring on time past conditions),
    persistent or secure-based (like CSRF tokens)</li>
  <li>Cats app: supports for user CRUD operations againt the database ORM objects using POST forms. Implements Form Cleaning and Validation</li>
  <li>Autos app: extends functionality of Cats app with user authentification requirement</li>
  <li>Ads app: extends functionality of Autos app with authorization requirement and user property filtering (i.e. you can only edit or delete ads created by you), also has support for user-queried search in ORM objects</li>
  <li>REST API: provides API endpoints for retrieving all registered Users and Groups in application/json format. Login required. Lookup for guest credentials at login page.
  <li>Social Login: an extenstion allowing you to login with your GitHub account, integrated with Django inside mysite/settings.py</li>
</ul>
