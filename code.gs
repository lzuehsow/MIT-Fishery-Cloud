function analyze(input) {
  var headers = {
  "X-Api-Key" : getAPIKey()
  }
  var options = {
  'method' : 'post',
  'headers': headers,
  'payload' : JSON.stringify(input),
  }
 
  var response = UrlFetchApp.fetch('https://mm9r0ap4mg.execute-api.us-east-1.amazonaws.com/prod', options);
 
  if (response.getResponseCode() != 200) {
    return "Could not process"
  } else {
    Logger.log(response.getContentText())
    return response.getContentText()
  }
}

function getAPIKey() {
  let token, endpoint, response;
  endpoint = `https://secretmanager.googleapis.com/v1/projects/983104801891/secrets/HerringSecret/versions/1:access`;
  token = ScriptApp.getOAuthToken();
  response = UrlFetchApp.fetch(endpoint, {
    headers: {
      Authorization: 'Bearer ' + token,
      Accept: 'application/json',
    }
  });
  var decodedAPIKey = Utilities.base64Decode(JSON.parse(response.getContentText())['payload']['data']);
  var apiKey = Utilities.newBlob(decodedAPIKey).getDataAsString()
  return apiKey;
}
