import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;

import javax.lang.model.util.Elements;
import javax.swing.text.Element;


import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;


public class something {

    // Method to send POST request with an image and prompt
    public static String sendPostRequest(String apiUrl, String prompt, String imagePath) {
        String boundary = "===" + System.currentTimeMillis() + "==="; // Boundary for multipart
        HttpURLConnection connection = null;

        try {
            // Open connection to the API URL
            URL url = new URL(apiUrl);
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setDoOutput(true);
            connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);

            // Write data to the request
            try (DataOutputStream outputStream = new DataOutputStream(connection.getOutputStream())) {
                // Add the prompt field
                writeFormField(outputStream, "prompt", prompt, boundary);

                // Add the image file field
                writeFileField(outputStream, "image", imagePath, boundary);

                // End boundary
                outputStream.writeBytes("--" + boundary + "--\r\n");
                outputStream.flush();
            }

            // Get the response from the API
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                String response = readResponse(connection.getInputStream());
                System.out.println("The response is          ::::::::"+response); 
                return response;// Print the response directly
            } else {
                String errorResponse = readResponse(connection.getErrorStream());
                System.out.println("Error Response: " + errorResponse);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
        return null;
    }

    // Helper method to write a form field (e.g., prompt)
    private static void writeFormField(DataOutputStream outputStream, String name, String value, String boundary) throws IOException {
        outputStream.writeBytes("--" + boundary + "\r\n");
        outputStream.writeBytes("Content-Disposition: form-data; name=\"" + name + "\"\r\n\r\n");
        outputStream.writeBytes(value + "\r\n");
    }

    // Helper method to write a file field (e.g., image)
    private static void writeFileField(DataOutputStream outputStream, String fieldName, String filePath, String boundary) throws IOException {
        File file = new File(filePath);
        outputStream.writeBytes("--" + boundary + "\r\n");
        outputStream.writeBytes("Content-Disposition: form-data; name=\"" + fieldName + "\"; filename=\"" + file.getName() + "\"\r\n");
        outputStream.writeBytes("Content-Type: " + Files.probeContentType(file.toPath()) + "\r\n\r\n");

        try (FileInputStream fileInputStream = new FileInputStream(file)) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fileInputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
            }
        }
        outputStream.writeBytes("\r\n");
    }

    // Helper method to read the response from an InputStream
    private static String readResponse(InputStream inputStream) throws IOException {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream))) {
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            return response.toString();
        }
    }

    // Main method to test the API call
    public static void main(String[] args) {
        String apiUrl = "http://localhost:8000/api/process-image-and-prompt/"; // Replace with your Django API URL
        String prompt = "Describe the image";
        String imagePath = "C:/Users/yarrampati ganesh/Desktop/dog_image.jpeg"; // Replace with the actual path to your image

       String r= sendPostRequest(apiUrl, prompt, imagePath);
       Document document = Jsoup.parse(r);

        // Extract the <body> content
        Element body = document.body();

        // Print the body content
        System.out.println("Body Content:");
        System.out.println(body.html());

    }
}

