import React, { useEffect, useState } from 'react';
import axios, { AxiosResponse, AxiosError } from 'axios';

interface Response {
  user_id: string;
  created_at: string;
  text: string;
}

function GetDynamodb() {
  const [data, setData] = useState<Response[]>([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/dynamodb')
      .then(function (response: AxiosResponse) {
        setData(response.data);
      })
      .catch(function (error: AxiosError) {
        console.error(error);
      });
  }, []);

  return (
    <div>
      {data && data.map((item, index) => (
        <div key={index}>
          <p>User ID: {item.user_id}</p>
          <p>Created At: {item.created_at}</p>
          <p>Text: {item.text}</p>
        </div>
      ))}
    </div>
  );
}

export default GetDynamodb;
