import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import storage from '../../../utils/local-storage';
import LoginComponent from '../../Login/login';
import MobileBooking from '../Booking/MobileBooking';
import withTracker from '../../HOC/withTracker';
import './Home.scss';


class HomeMobile extends Component {
  componentDidMount = () => {
    document.title = 'Home';
  }

  render() {
    const user = storage.getUser();

    return (
      <div className="mobileLogin__container">
        <h1> Capstone Reservation </h1>
        { user ? null : <LoginComponent /> }
        <Link to="/?forceDesktop=true">Calendar/Desktop version</Link>
        <div>
          <MobileBooking />
        </div>
      </div>
    );
  }
}

export default withTracker(HomeMobile);
