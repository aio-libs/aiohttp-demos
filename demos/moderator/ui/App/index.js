import "whatwg-fetch";
import { h, render, Component } from "preact";
import classNames from "./App.scss";
import Results from "./Results";

class App extends Component {
  constructor() {
    super();

    this.state = {
      comment: "",
      toxic: 0,
      severe_toxic: 0,
      obscene: 0,
      threat: 0,
      insult: 0,
      identity_hate: 0
    };

    this.handleInput = this.handleInput.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInput(event) {
    this.setState({
      comment: event.target.value
    });
  }

  handleSubmit(event) {
    event.preventDefault();
    fetch("/moderate", {
      method: "POST",
      body: JSON.stringify([{ comment: this.state.comment }])
    })
      .then(response => response.text())
      .then(jsonData => JSON.parse(jsonData))
      .then(data => {
        this.setState({
          toxic: data[0].toxic,
          severe_toxic: data[0].severe_toxic,
          obscene: data[0].obscene,
          threat: data[0].threat,
          insult: data[0].insult,
          identity_hate: data[0].identity_hate
        });
      });
  }

  render() {
    return (
      <main className={classNames.main}>
        <h1>Moderator AI</h1>

        <Results
          toxic={this.state.toxic}
          severe_toxic={this.state.severe_toxic}
          obscene={this.state.obscene}
          threat={this.state.threat}
          insult={this.state.insult}
          identity_hate={this.state.identity_hate}
        />

        <form
          className={classNames.form}
          onSubmit={this.handleSubmit}
          autocomplete="off"
        >
          <textarea
            className={classNames.textarea}
            onInput={this.handleInput}
            name="comment"
            placeholder="Comment"
            autofocus
          />

          <button type="submit" className={classNames.submit}>
            Submit
          </button>
        </form>
      </main>
    );
  }
}

render(<App />, document.body);
