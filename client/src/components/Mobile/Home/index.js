import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'semantic-ui-react';
import storage from '../../../utils/local-storage';
import LoginComponent from '../../Login/login';
import MobileBooking from '../Booking/MobileBooking';
import withTracker from '../../HOC/withTracker';
import './Home.scss';


class HomeMobile extends Component {
  state = {
    createBooking: false,
  }

  componentDidMount = () => {
    document.title = 'Home';
  }

  handleMakeBooking = () => {
    this.setState({
      createBooking: true,
    });
  }

  finishBooking = () => {
    this.setState({
      createBooking: false,
    });
  }

  render() {
    const user = storage.getUser();
    const {
      createBooking,
    } = this.state;

    return (
      <div className="mobileLogin__container">
        <h1> Capstone Reservation </h1>
        { user ? null : <LoginComponent /> }
        <div>
          <Button>
            <Link to="/?forceDesktop=true">Calendar/Desktop version</Link>
          </Button>
          { createBooking ? null : <Button content="Create Booking" primary onClick={this.handleMakeBooking} /> }
          { createBooking ? <MobileBooking finishBooking={this.finishBooking} /> : null }
        </div>
      </div>
    );
  }
}

export default withTracker(HomeMobile);
