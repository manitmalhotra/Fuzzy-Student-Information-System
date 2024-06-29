package FuzzyStudentInformationSystem;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.Map;
import org.json.JSONObject;

public class predit {

    public String pre(double marks, double attend) {
        try {
            // Define the Python script and arguments
            String pythonScriptPath = "fuzzy_logic.py"; // Update with your actual script path
            JSONObject inputData = new JSONObject();
            inputData.put("attendance", attend); // Use the provided attendance parameter
            inputData.put("marks", marks);

            // Example path, adjust based on your Python installation
            String pythonInterpreter = "C:\\Users\\manit\\AppData\\Local\\Programs\\Python\\Python311\\python.exe";

            // Create the process builder with the full path to the Python executable
            ProcessBuilder pb = new ProcessBuilder(pythonInterpreter, pythonScriptPath);
            Map<String, String> env = pb.environment();
            pb.redirectErrorStream(true);

            // Start the process
            Process process = pb.start();

            // Write the input data to the Python process
            process.getOutputStream().write(inputData.toString().getBytes());
            process.getOutputStream().flush();
            process.getOutputStream().close();

            // Capture the output
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));

            // Read the output from the command
            StringBuilder output = new StringBuilder();
            String s;
            while ((s = stdInput.readLine()) != null) {
                output.append(s);
            }

            // Wait for the process to complete
            int exitCode = process.waitFor();
            System.out.println("Process exited with code: " + exitCode);

            // Print the output for debugging
            System.out.println("Python script output: " + output.toString());

            // Parse and print the result
            JSONObject result = new JSONObject(output.toString());
            System.out.println("Outcome of risk is: " + result.getDouble("result"));
            double risk = result.getDouble("result");
            long roundedRisk = Math.round(risk); // Round the risk value
                return String.valueOf(roundedRisk);
            

        } catch (Exception e) {
            e.printStackTrace();
        }
        
            return null;
    }
}












