function onFormSubmit(e) {
  const webhookUrl = "http://ec2-44-201-203-146.compute-1.amazonaws.com:5000/webhook"; // Replace with your Flask app's URL
  

  // Send the data to the Flask app
  const options = {
    method: "POST",
  };

  try {
    const response = UrlFetchApp.fetch(webhookUrl, options);
    Logger.log("Response from Flask app: " + response.getContentText());
  } catch (error) {
    Logger.log("Error sending data: " + error.message);
  }
}