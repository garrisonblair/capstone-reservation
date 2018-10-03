import React, {Component} from 'react';
import settings from '../../config/settings';
import './Home.scss';
import Calendar from '../Calendar';


class Home extends Component {
  componentDidMount() {
    console.log(settings)
  }

  render() {
    return (
      <div>
        <main>
          <Calendar/>
        </main>
        
      </div>      
    )
  }
}

export default Home;
