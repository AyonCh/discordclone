import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [name, setName] = useState("");
  const [data, setData] = useState([]);

  const sse = new EventSource("http://localhost:5000/msg");
  sse.onmessage = (e) => {
    console.log(e);
    setData([...data, JSON.parse(e.data)]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    await (
      await fetch("http://localhost:5000/post", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: input,
          author: name,
        }),
      })
    ).json();
  };

  return (
    <>
      <div className="chat">
        {data.map((msg, k) => (
          <div key={k}>
            <p>
              <b>{msg.author}</b>: {msg.message}
            </p>
          </div>
        ))}
      </div>
      <form onSubmit={(e) => handleSubmit(e)}>
        <input
          type="text"
          placeholder="message"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
      </form>
    </>
  );
}

export default App;
