import PropTypes from 'prop-types';
import React, {Component} from 'react';
import {Button, Dropdown, Header, Icon, Modal} from 'semantic-ui-react';
import CampOnForm from './CampOnForm.js';
import EditBookingForm from './EditBookingForm.js';
import './BookingInfoModal.scss';


class BookingInfoModal extends Component {
  state = {
    show: false,
  }

  closeModal = () => {
    this.props.onClose();
    this.setState({
      show: false
    });
  }

  //Close the modal if any api POST requests succeeded
  closeModalWithAction = () => {
    this.setState({
      show: false,
    });
    this.props.onCloseWithAction();
  }

  handleOpen = () => this.setState({show: true});

  checkCamponPossible(booking) {
    if(booking.id) {
      let currentDate = new Date();
      let currentTime = `${currentDate.getHours()}${currentDate.getMinutes() < 10 ? `0${currentDate.getMinutes()}` : `${currentDate.getMinutes()}`}`;
      let bookingEndTime = booking.end_time.replace(/:/g, '');
      bookingEndTime = bookingEndTime / 100;
      if(currentTime < bookingEndTime) {
        return true;
      } else {
        return false;
      }
    } else {
      return false;
    }
  }

  checkSameUser(booking) {
    if (localStorage.getItem("CapstoneReservationUser") && !!booking.booker) {
      return booking.booker.user.username == JSON.parse(localStorage.getItem("CapstoneReservationUser")).username
    }
  }

  /************* COMPONENT LIFE CYCLE *************/

  componentWillReceiveProps(nextProps) {
    if(nextProps.show) {
      this.setState({
        show: nextProps.show
      });
    }
  }

  /************* COMPONENT RENDERING *************/

  renderDescription() {
    const {booking} = this.props;
    let camponPossible = this.checkCamponPossible(booking);

    return (
      <Modal.Content>
        <Modal.Description>
          <Header>
            {booking.date}
          </Header>
          <div className="modal-description">
            <h3 className="header--inline">
              {`from ${booking.start_time ? booking.start_time.slice(0,-3) : ''}`}
            </h3>
          </div>
          <div className="modal-description">
            <h3 className="header--inline">
              {`to ${booking.end_time? booking.end_time.slice(0,-3) : ''}`}
            </h3>
          </div>
          <div className="modal-description">
            <h3 className="header--inline">
              <Icon name="user" /> {" "}
              {!!booking.booker ? `by ${booking.booker.user.username}` : ''}
            </h3>
          </div>
          <div className="ui divider" />
          {this.renderForm(booking)}
          <div>
            <Button content='Close' secondary onClick={this.closeModal} />
          </div>
        </Modal.Description>
      </Modal.Content>
    )
  }

  renderForm(booking) {
    if(this.checkSameUser(booking)) {
      return <EditBookingForm booking={booking} selectedRoomName={this.props.selectedRoomName} onCloseWithEditBooking={this.closeModalWithAction}/>
    } else {
      if(this.checkCamponPossible(booking)) {
        return <CampOnForm booking={booking} selectedRoomName={this.props.selectedRoomName} onCloseWithCampOn={this.closeModalWithAction}/>
      } else {
        return null
      }
    }
  }

  render() {
    const {show} = this.state;
    const {selectedRoomName} = this.props;
    return (
      <div id="reservation-details-modal">
        <Modal centered={false} size={"tiny"} open={show}>
          <Modal.Header>
            <Icon name="map marker alternate" />
            Room {selectedRoomName}
          </Modal.Header>
          {this.renderDescription()}
        </Modal>
      </div>
    )
  }
}

BookingInfoModal.propTypes = {
  show: PropTypes.bool.isRequired,
  booking: PropTypes.object.isRequired,
  selectedRoomName: PropTypes.string.isRequired,
  onClose: PropTypes.func,
  onCloseWithCampOn: PropTypes.func,
}

export default BookingInfoModal;
