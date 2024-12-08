function onFormSubmit(e) {
    // Check if 'e' and 'e.values' are defined
    if (!e || !e.values || e.values.length === 0) {
      Logger.log("No responses received or 'e.values' is undefined");
      return;
    }
  
    const webhookUrl = "http://192.168.1.14:5000/";
    UrlFetchApp.fetch(webhookUrl);
  }
  