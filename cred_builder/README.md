All of these files go into the same folder on macOS. 

```
googleAuth.js
credentials.json
package.json
package-lock.json
```
credentials.json can be produced at [Gmail > API > Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)


You must have [Node.js](https://nodejs.org/en/) & [NPM](https://www.npmjs.com/) installed

In the folder you will follow these steps in a terminal window.

```
npm i
node googleAuth.js
```

Follow the instructions in the terminal.

This will produce token.json file for your specific email account that can be used within the DS web-based API.