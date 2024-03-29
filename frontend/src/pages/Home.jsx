import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "../App.css";
import axios from "axios";

export const Home = () => {
  const [input, setInput] = useState("");
  const [name, setName] = useState("");
  const [data, setData] = useState([]);
  const { id } = useParams();

  useEffect(() => {
    if (id) {
      let sse = new EventSource("http://localhost:5000/msg");
      sse.onmessage = (e) => {
        setData((data) => [...data, JSON.parse(e.data)]);
      };
      sse.onopen = () => {
        setData([]);
      };
    }
  }, []);

  useEffect(() => {
    if ((data.length > 0) & id) {
      let message = document.getElementById(String(data.length - 1));
      message.scrollIntoView();
    }
  }, [data]);

  if (!id) {
    return (
      <div className="imgine">
        <div className="imagine">Imaging having friends</div>;
      </div>
    );
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(input);
    axios.post("http://localhost:5000/post", {
      message: input.trim(),
      author: name,
      time: new Date().toLocaleTimeString().slice(0, 5),
    });
    setInput("");
  };

  return (
    <>
      <nav>Some</nav>
      <div className="chat">
        {data.map((msg, k) => (
          <div className="message" key={k} id={k}>
            {k > 0 ? (
              data[k - 1].author == msg.author ? (
                <></>
              ) : (
                <div className="title">{msg.author}</div>
              )
            ) : (
              <div className="title">{msg.author}</div>
            )}
            <div className="text">
              <div className="time">{msg.time}</div>
              <div className="msg">
                {msg.message.startsWith("https") ? (
                  <a href={msg.message} target="_blank">
                    {msg.message}
                  </a>
                ) : (
                  <>{msg.message}</>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      <input
        type="text"
        placeholder="username"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <form className="input" onSubmit={(e) => handleSubmit(e)}>
        <input
          type="text"
          placeholder="message"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
      </form>
    </>
  );
};
