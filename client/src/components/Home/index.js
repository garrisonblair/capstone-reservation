import React, { Component } from 'react';
import './Home.scss';
import Calendar from '../Calendar';


class Home extends Component {
  componentDidMount = () => {
    document.title = 'Home';
  }

  render() {
    return (
      <div>
        <main>
          <Calendar />
        </main>
      </div>
    );
  }
}

export default Home;
