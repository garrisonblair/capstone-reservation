import PropTypes from 'prop-types';
import React, {Component} from 'react';
import {Button, Dropdown, Header, Icon, Modal} from 'semantic-ui-react';
import CampOnForm from './CampOnForm.js';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
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

  closeModalWithCampOn = () => {
    this.props.onCloseWithCampOn();
    this.setState({
      show: false,
    });
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
    const {booking, selectedRoomName} = this.props;
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
              {`by ${booking.booker}`}
            </h3>
          </div>
          <div className="ui divider" />
          {camponPossible ? <CampOnForm booking={booking} selectedRoomName={selectedRoomName} onCloseWithCampOn={this.closeModalWithCampOn}/> : null}
          <div>
            <Button content='Close' secondary onClick={this.closeModal} />
          </div>
        </Modal.Description>
      </Modal.Content>
    )
  }

  renderCampOnForm() {
    const {hourOptions, minuteOptions, reservedOptions, endHour, endMinute} = this.state;
    return(
      <div>
        <div className="modal-description">
          <h3 className="header--inline">
            <span>Camp on until  </span>
          </h3>
          <Dropdown
            selection
            compact
            className="dropdown--fixed-width"
            placeholder='hh'
            options={hourOptions}
            onChange={this.handleEndHourChange}
            defaultValue={endHour}
          />
          <Dropdown
            selection
            compact
            className="dropdown--fixed-width"
            placeholder='mm'
            options={minuteOptions}
            onChange={this.handleEndMinuteChange}
            defaultValue={endMinute}
          />
        </div>
        <div className="modal-description">
            <h3 className="header--inline">
              <Icon name="user" /> {" "}
              {`by `}
            </h3>
            <Dropdown
              selection
              compact
              className="dropdown--fixed-width"
              placeholder='hh'
              options={reservedOptions}
              defaultValue={reservedOptions[0].value}
            />
          </div>
          <Button content='Camp on' primary onClick={this.handleSubmit} />
          <div className="ui divider" />
      </div>

    )
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
