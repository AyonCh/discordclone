import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "../App.css";
import axios from "axios";

export const Home = () => {
  const [input, setInput] = useState("");
  const [name, setName] = useState("");
  const [data, setData] = useState([]);

  let sse;

  useEffect(() => {
    sse = new EventSource("http://localhost:5000/msg");
    sse.onmessage = (e) => {
      setData((data) => [...data, JSON.parse(e.data)]);
    };
    sse.onopen = () => {
      setData([]);
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(input);
    axios.post("http://localhost:5000/post", {
      message: input,
      author: name,
      time: new Date().toLocaleTimeString().slice(0, 5),
    });
    setInput("");
  };

  const { id } = useParams();
  if (!id) {
    return <>NO</>;
  }
  return (
    <div>
      <div className="chat">
        {data.map((msg, k) => (
          <div key={k}>
            <p>
              <b>
                {msg.time} {msg.author}
              </b>
              : {msg.message}
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
      <input
        type="text"
        placeholder="username"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
    </div>
  );
};
