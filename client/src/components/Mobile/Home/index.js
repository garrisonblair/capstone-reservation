import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Button } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import storage from '../../../utils/local-storage';
import LoginComponent from '../../Login/login';
import MobileBooking from '../Booking/MobileBooking';
import MobileDashboard from '../Dashboard';
import api from '../../../utils/api';
import './Home.scss';


class HomeMobile extends Component {
  state = {
    createBooking: false,
    isLoggedIn: false,
  }

  componentDidMount = () => {
    document.title = 'Home';
    const user = storage.getUser();
    let isLoggedIn = false;
    if (user) {
      isLoggedIn = true;
    }
    this.setState({
      isLoggedIn,
    });
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

  onSuccess = () => {
    this.setState({
      isLoggedIn: true,
    });
  }

  handleLogout = () => {
    api.logout()
      .then(() => {
        sweetAlert.fire({
          position: 'top',
          type: 'success',
          title: 'Logged out',
          toast: true,
          showConfirmButton: false,
          timer: 2000,
        });

        this.setState({ isLoggedIn: false });
      });
  }

  renderCreateBooking() {
    return (
      <div className="mobileLogin__body">
        <MobileBooking finishBooking={this.finishBooking} />
      </div>
    );
  }

  renderMobileDashboard = () => (
    <div>
      <MobileDashboard />
    </div>
  )

  renderLoggedInPage() {
    const {
      createBooking,
    } = this.state;

    return (
      <div>
        {createBooking ? this.renderCreateBooking() : null}
        <div>
          {this.renderMobileDashboard()}
        </div>
      </div>
    );
  }

  render() {
    const {
      createBooking,
      isLoggedIn,
    } = this.state;

    return (
      <div className="mobileLogin__container">
        <div className="mobileLogin__top">
          <h1 className="topBar"><center> Capstone Rooms </center></h1>
          { isLoggedIn ? null : <LoginComponent onSuccess={this.onSuccess} /> }
          <div>
            <center>
              <Link to="/?forceDesktop=true">
                <Button className="desktopButton"> Calendar </Button>
              </Link>
              { (!isLoggedIn || createBooking) ? null : <Button className="mainButton book" content="Create Booking" primary onClick={this.handleMakeBooking} /> }
            </center>
          </div>
        </div>
        <div>
          { isLoggedIn ? this.renderLoggedInPage() : null }
          <br />
          { isLoggedIn ? (
            <center>
              <Button className="mobile_button-logout" onClick={this.handleLogout}>
                Logout
              </Button>
            </center>) : null }
        </div>
      </div>
    );
  }
}

export default HomeMobile;
