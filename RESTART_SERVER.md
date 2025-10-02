# How to Restart Your Server to Enable Opik Tracing

## The Issue

Your server is currently running with the OLD code that had the broken import. You need to restart it to load the FIXED code.

## Steps to Restart

### 1. Stop the Current Server

Find and stop any running Python server:

**Option A: If you started it in a terminal**

- Go to that terminal window
- Press `Ctrl+C` to stop the server

**Option B: If you can't find the terminal**

```bash
# Find the process
ps aux | grep "python.*index.py" | grep -v grep

# Kill it (replace PID with the actual process ID from above)
kill <PID>
```

### 2. Start the Server with the Fixed Code

```bash
cd api
python index.py
```

You should see output like:

```
INFO:comet_client:✓ Opik SDK imported successfully
INFO:comet_client:Opik Configuration Check:
INFO:comet_client:  API Key present: True
INFO:comet_client:  Project Name: careerpathai
INFO:comet_client:Initializing Opik client with project: careerpathai
INFO:comet_client:✓ Opik client initialized successfully for project: careerpathai
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Test the API

In a NEW terminal window:

```bash
cd api
python test_api_trace.py
```

This will:

1. Make a real API call to your server
2. Verify the response is successful
3. Confirm that traces are being sent to Opik

### 4. Check Your Dashboard

After the test succeeds:

1. Go to https://www.comet.com/opik/
2. Navigate to your "careerpathai" project
3. You should see a new trace for the API call!

### 5. Test with Your Frontend

Now try clicking "Generate Path" in your frontend. You should see:

- The API responds successfully
- A new trace appears in your Opik dashboard

## Troubleshooting

### If you still don't see traces:

1. **Check the server logs** - Look for these lines when you make a request:

   ```
   INFO:comet_client:Started trace: career_path_generation
   OPIK: Started logging traces to the "careerpathai" project
   ```

2. **Verify environment variables** - Make sure your `.env` file is in the project root:

   ```bash
   cat .env | grep COMET
   ```

3. **Check for errors** - Look for any error messages in the server logs

4. **Run the diagnostic test**:
   ```bash
   cd api
   python test_comet.py
   ```

## Quick Restart Command

```bash
# Stop any running server and start fresh
pkill -f "python.*index.py" 2>/dev/null; cd api && python index.py
```
