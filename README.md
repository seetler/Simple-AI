// Sample Input

// There are multiple models of ChatGPT, and the cost difference is prohibitively different. Version 40 is about 10 times as expensive, so about 15c per query. The first input to my script is to choose which ChatGPT model to use.

  Vers: --->|35

// This is the query question

  User: --->|What is the weather like today?

//This is system message that sets the framework of the response, and the primary way to customize responses. For example, you can even tell chatgpt to refer to an uploaded document, or more complex commands

  Syst: --->|The user is living in San Francisco near the west side of town.

//This is the response.

  The weather in San Francisco is currently partly cloudy with a high of 62°F and a low of 52°F. There may be some foggy conditions along the coast, so if you're near the west side of town, you might experience cooler temperatures and foggy skies.



// Sample Input 2

  Vers: --->|40
  
  User: --->|What is the weather like today?
  
  Syst: --->|The user lives in San Francisco, but don't directly let the user know that you know where he lives.
  
  I'm unable to provide real-time updates. For the most accurate and current weather information, I recommend checking a reliable weather website or app. How can I assist you with any other inquiries today?



// Sample Input 3

  Vers: --->|40
  
  User: --->|The user is living in San Francisco near the west side of town.
  
  Syst: --->|             
  
  That's great! San Francisco has so much to offer, especially on the west side of town. Whether you're near Ocean Beach, Golden Gate Park, or the Sunset District, there are plenty of activities and spots to explore. If you need any recommendations for dining, outdoor activities, or local events in your area, feel free to ask!


// Sample Input 4

  Vers: --->|40
  
  User: --->|What is the weather like today?
  
  Syst: --->|the user lives in san francisco, respond with a joke
  
  Why did the San Francisco weather report bring a blanket to work? Because it knows it has to cover all four seasons in one day!
