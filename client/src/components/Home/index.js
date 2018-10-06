import React, {Component} from 'react';
import settings from '../../config/settings';
import './Home.scss';


class Home extends Component {
  componentDidMount = () => {
    document.title = 'Home'
  }

  render() {
    return (
      <div id="home">
        <h1> Home </h1>
      </div>
    )
  }
}

export default Home;
