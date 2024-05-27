import { useState } from "react";

const Search = () => {
  const [data, setData] = useState("Initial data");
  const testAPI = async () => {
    try {
      // make request
      const response = await fetch("http://127.0.0.1:5000", {
        method: "GET",
        headers: {
          "Content-type": "application/json",
        },
      });

      // if response not ok
      if (!response.ok) {
        console.log("RESPONSE IS NOT OK");
        throw new Error("Failed to fetch data");
      }

      // read response
      const newData = await response.json();
      console.log("newData:" + newData);
      setData(JSON.stringify(newData));

      // error handling
    } catch (error) {
      console.log("CANNOT FETCH");
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div>
      <div>
        <p>Data: {data} </p>
        <p>Hello this is search!</p>
        <input
          type="search"
          name="search-form"
          className="search-input"
          placeholder="Search ingredient"
        />
        <button onClick={testAPI}>Click to change data!</button>
      </div>
    </div>
  );
};

export default Search;
