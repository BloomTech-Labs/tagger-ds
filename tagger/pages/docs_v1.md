# Taggermail Data Science Documentation <img src="../static/markdown-logo.png" height=20, width=32></img>


## Accessing the API Endpoints

### /api/sync
Input:
```python
{   
    "provider": <email service>,
    "token": [
        {
            "refresh_token": <refresh_token_value>,
            "client_id": <client_id_value>,
            "client_secret": <client_secret_value>,
        },
        ...
    ]
}



```
Output:
```

```


- "emails" array can have a length > 0, but only the first entry will be taken.
- This endpoint can also be used for predicting what real emails are closest to a hypothetical email.

Output:
```
Array of 5 email UID's closest in content to the selected email
or "No model in database for this address..."
```
