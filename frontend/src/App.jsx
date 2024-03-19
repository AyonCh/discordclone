import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios"

function App() {
  const [input, setInput] = useState("");
  const [name, setName] = useState("");
  const [data, setData] = useState([]);

    var sse;

  useEffect(() => {
    sse = new EventSource("http://localhost:5000/msg");
    sse.onmessage = (e) => {
        console.log(e.data);
        console.log([...data, JSON.parse(e.data)])
        setData(data => [...data, JSON.parse(e.data)]);
      };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    axios.post("http://localhost:5000/post", {
        message: input,
        author: name,
      })
  };

  return (
    <>
      <div className="chat">
        {data.map((msg, k) => {
            console.log("Good morning", msg)
            return (
            <div key={k}>
                <p>
                <b>{msg.author}</b>: {msg.message}
                </p>
            </div>
          )
        })}
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
