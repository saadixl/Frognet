import http from 'node:http';
const env = process.env;

const options = {
  hostname: env.TODOIST_API_HOSTNAME,
  port: env.TODOIST_API_PORT,
  path: `/${env.TODOIST_API_PATH}`,
  method: 'POST',
};

export {handle};

function callApi() {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
        console.log(`statusCode: ${res.statusCode}`);
        res.on('data', (data) => {
          resolve({
            data: JSON.stringify(data)
          });
        });
    });

    req.on('error', (error) => {
      resolve({
        error: JSON.stringify(error)
      });
    });

    req.end();
  });
}

async function handle (event, context, cb) {
  await callApi();
  const response = {
    message: 'OK'
  };
  return response;
};
