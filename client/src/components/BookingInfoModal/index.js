import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {
  Button,
  Icon,
  Modal,
} from 'semantic-ui-react';
import CampOnForm from './CampOnForm';
import EditBookingForm from './EditBookingForm';
import './BookingInfoModal.scss';


class BookingInfoModal extends Component {
  static checkCamponPossible(booking) {
    if (booking.id) {
      const currentDate = new Date();
      const currentTime = `${currentDate.getHours()}${currentDate.getMinutes() < 10 ? `0${currentDate.getMinutes()}` : `${currentDate.getMinutes()}`}00`;
      const bookingEndTime = booking.end_time.replace(/:/g, '');
      const bookingStartTime = booking.start_time.replace(/:/g, '');
      if (currentTime < bookingEndTime && currentTime > bookingStartTime) {
        return true;
      }
      return false;
    }
    return false;
  }

  static checkSameUser(booking) {
    if (localStorage.getItem('CapstoneReservationUser') && !!booking.booker) {
      return booking.booker.username === JSON.parse(localStorage.getItem('CapstoneReservationUser')).username;
    }
    return false;
  }

  state = {
    show: false,
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.show) {
      this.setState({
        show: nextProps.show,
      });
    }
  }

  closeModal = () => {
    const { onClose } = this.props;
    onClose();
    this.setState({
      show: false,
    });
  }

  // Close the modal if any api POST requests succeeded
  closeModalWithAction = () => {
    const { onCloseWithAction } = this.props;
    this.setState({
      show: false,
    });
    onCloseWithAction();
  }

  handleOpen = () => this.setState({ show: true });

  renderCampons = () => {
    const { campons } = this.props;
    const camponsInfo = [];
    campons.forEach((campon, index) => {
      camponsInfo.push(
        <h3 className="header--inline" key={campon.id}>
          {`${index + 1}. ${campon.booker.username}: ${campon.start_time.slice(0, -3)} -  ${campon.end_time.slice(0, -3)}`}
          <br />
        </h3>,
      );
    });
    return (
      <div className="modal-description--campons">
        <h3 className="header--inline">
          Campons:
        </h3>
        <div>
          {camponsInfo}
        </div>
      </div>
    );
  }

  renderDescription() {
    const { booking, campons } = this.props;
    const booker = !!booking.booker;
    return (
      <Modal.Content>
        <Modal.Description>
          <div className="modal-description__container">
            <div className="modal-description--details">
              <h3 className="header--inline">
                {booking.date}
              </h3>
              <div className="modal-description">
                <h3 className="header--inline">
                  {`from ${booking.start_time ? booking.start_time.slice(0, -3) : ''}`}
                </h3>
              </div>
              <div className="modal-description">
                <h3 className="header--inline">
                  {`to ${booking.end_time ? booking.end_time.slice(0, -3) : ''}`}
                </h3>
              </div>
              <div className="modal-description">
                <h3 className="header--inline">
                  <Icon name="user" />
                  {' '}
                  {booker ? `by ${booking.booker.username}` : ''}
                </h3>
              </div>
            </div>
            {campons == null || campons.length === 0 ? null : this.renderCampons()}
          </div>
          <div className="ui divider" />
          {this.renderForm(booking)}
          <div>
            <Button content="Close" secondary onClick={this.closeModal} />
          </div>
        </Modal.Description>
      </Modal.Content>
    );
  }

  renderForm(booking) {
    const { selectedRoomName } = this.props;
    if (BookingInfoModal.checkSameUser(booking)) {
      return (
        <EditBookingForm
          booking={booking}
          selectedRoomName={selectedRoomName}
          onCloseWithEditBooking={this.closeModalWithAction}
        />);
    }
    if (BookingInfoModal.checkCamponPossible(booking)) {
      return (
        <CampOnForm
          booking={booking}
          selectedRoomName={selectedRoomName}
          onCloseWithCampOn={this.closeModalWithAction}
        />);
    }
    return null;
  }

  render() {
    const { show } = this.state;
    const { selectedRoomName } = this.props;
    return (
      <div id="reservation-details-modal">
        <Modal centered={false} size="tiny" open={show} onClose={this.closeModal}>
          <Modal.Header>
            <Icon name="map marker alternate" />
            Room&nbsp;
            {selectedRoomName}
          </Modal.Header>
          {this.renderDescription()}
        </Modal>
      </div>
    );
  }
}

BookingInfoModal.propTypes = {
  show: PropTypes.bool.isRequired,
  booking: PropTypes.instanceOf(Object).isRequired,
  selectedRoomName: PropTypes.string.isRequired,
  onClose: PropTypes.func,
  onCloseWithAction: PropTypes.func,
  campons: PropTypes.instanceOf(Array),
};

BookingInfoModal.defaultProps = {
  onClose: () => {},
  onCloseWithAction: () => {},
  campons: null,
};

export default BookingInfoModal;
