import PropTypes from 'prop-types';
import React, { Component } from 'react';
import {
  Button, Dropdown, Header, Icon, Form, Input, Modal, Checkbox, Tab,
} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import './ReservationDetailsModal.scss';
import toDateInputValue from '../../utils/dateFormatter';
import Login from '../Login';
import api from '../../utils/api';

class ReservationDetailsModal extends Component {
  state = {
    show: false,
    showLogin: false,
    startHour: '8',
    startMinute: '00',
    endHour: '8',
    endMinute: '30',
    hourOptions: [],
    reservedOptions: [],
    isRecurring: false,
    tabIndex: 0,
    inputOption0: {
      startDate: '',
      endDate: '',
    },
    reservationProfiles: ['me'],
  }

  componentWillMount() {
    const {
      minHour, maxHour, minuteInterval, selectedDate,
    } = this.props;
    const { reservationProfiles } = this.state;
    this.setState({
      hourOptions: this.generateHourOptions(minHour, maxHour),
      minuteOptions: this.generateMinuteOptions(minuteInterval),
      reservedOptions: this.generateReservationProfilesOptions(reservationProfiles),
      inputOption0: {
        startDate: toDateInputValue(selectedDate),
        endDate: toDateInputValue(selectedDate),
      },
    });
  }

  componentWillReceiveProps(nextProps) {
    const { show } = nextProps;
    if (nextProps.show) {
      this.setState({
        show,
      });
    }

    let hour = '';
    let minute = '';
    if (nextProps.selectedHour !== '') {
      [hour, minute] = nextProps.selectedHour.replace('AM', '').replace('PM', '').trim().split(':');

      // Removes leading zero
      if (hour.charAt(0) === '0') {
        hour = hour.substring(1, 3);
      }

      // Handle 24-hour military time
      if (nextProps.selectedHour.includes('PM') && hour !== '12') {
        hour = `${(parseInt(hour, 10) + 12)}`;
      }
    }
    this.setState({
      startHour: hour,
      startMinute: minute,
    });
    this.getDefaultEndTime(hour, minute);
  }

  generateHourOptions = (minHour, maxHour) => {
    const result = [];
    for (let i = minHour; i < maxHour; i += 1) {
      result.push({
        text: `${i}`,
        value: `${i}`,
      });
    }
    return result;
  }

  generateMinuteOptions = (minuteInterval) => {
    const result = [];
    for (let i = 0; i < 60; i += minuteInterval) {
      result.push({
        text: `${i < 10 ? `0${i}` : i}`,
        value: `${i < 10 ? `0${i}` : i}`,
      });
    }
    return result;
  }

  getDefaultEndTime = (startHour, startMinute) => {
    if (startHour !== '' && startMinute !== '') {
      let hour = parseInt(startHour, 10);
      let minute = parseInt(startMinute, 10);
      if (minute >= 30) {
        hour += 1;
        minute -= 30;
      } else {
        minute += 30;
      }
      hour = hour.toString(10);
      minute = minute.toString(10);
      this.setState({ endHour: hour, endMinute: minute });
    }
  }

  // TODO: This method needs to be changed when accessing groups
  generateReservationProfilesOptions = r => r.map(profile => ({ text: profile, value: profile }))

  closeModal = () => {
    const { onClose, selectedDate } = this.props;
    onClose();
    this.setState({
      inputOption0: {
        startDate: toDateInputValue(selectedDate),
        endDate: toDateInputValue(selectedDate),
      },
      show: false,
      isRecurring: false,
    });
  }

  closeModalWithReservation = () => {
    const { onCloseWithReservation } = this.props;
    onCloseWithReservation();
    this.setState({
      show: false,
    });
  }

  closeLogin = () => {
    const { isRecurring } = this.state;
    this.setState({ showLogin: false });
    if (localStorage.getItem('CapstoneReservationUser') == null) {
      sweetAlert(
        'Reservation failed',
        'Please Log in to make a reservation.',
        'error',
      );
    } else if (isRecurring) {
      this.sendPostRequestRecurringBooking(false);
    } else {
      this.sendPostRequestBooking();
    }
  }

  handleOpen = () => this.setState({ show: true });

  handleStartHourChange = (e, { value }) => {
    this.setState({
      startHour: value,
    });
  }

  handleStartMinuteChange = (e, { value }) => {
    this.setState({
      startMinute: value,
    });
  }

  handleEndHourChange = (e, { value }) => {
    this.setState({
      endHour: value,
    });
  }

  handleEndMinuteChange = (e, { value }) => {
    this.setState({
      endMinute: value,
    });
  }

  verifyEndTime = () => {
    const { endHour, endMinute } = this.state;
    if (endHour === '-1' || endMinute === '-1') {
      throw new Error('Please provide an end time to make a reservation.');
    }
  }

  verifyReservationTimes = () => {
    const {
      startHour, startMinute, endHour, endMinute,
    } = this.state;
    const startTime = `${startHour}.${startMinute}`;
    const endTime = `${endHour}.${endMinute}`;
    if (parseFloat(startTime) > parseFloat(endTime)) {
      throw new Error('Please provide a start time that is before the end time to make a reservation.');
    }
  }

  handleTabChange = (e, { activeIndex }) => {
    this.setState({ tabIndex: activeIndex });
  }

  verifyRecurringOption0 = () => {
    const { inputOption0 } = this.state;
    if (inputOption0.endDate == null) {
      throw new Error('Please enter an end date.');
    }
    if (!(new Date(inputOption0.startDate) < new Date(inputOption0.endDate))) {
      throw new Error('End date should be after starting date.');
    }
  }

  sendPostRequestBooking = () => {
    const { selectedDate, selectedRoomId, selectedRoomName } = this.props;
    const {
      startHour, startMinute, endHour, endMinute,
    } = this.state;
    // Handle time zone
    const tzoffset = (selectedDate).getTimezoneOffset() * 60000;
    const date = new Date(selectedDate - tzoffset);
    const localISOTime = date.toISOString().slice(0, -1);

    const data = {
      room: selectedRoomId,
      date: localISOTime.slice(0, 10),
      start_time: `${startHour}:${startMinute}:00`,
      end_time: `${endHour}:${endMinute}:00`,
    };
    api.createBooking(data)
      .then(() => {
        sweetAlert('Completed',
          `Room ${selectedRoomName} was successfuly booked.`,
          'success')
          .then(() => {
            this.closeModalWithReservation();
          });
      })
      .catch((error) => {
        sweetAlert(
          'Reservation failed',
          error.response.data,
          'error',
        );
      });
  }

  sendPostRequestRecurringBooking = (skipConflicts) => {
    const {
      startHour, endHour, startMinute, endMinute, inputOption0,
    } = this.state;
    const { selectedRoomId, selectedRoomName } = this.props;
    const user = JSON.parse(localStorage.CapstoneReservationUser);

    const data = {
      start_date: inputOption0.startDate,
      end_date: inputOption0.endDate,
      booking_start_time: `${startHour}:${startMinute}`,
      booking_end_time: `${endHour}:${endMinute}`,
      room: selectedRoomId,
      group: '',
      booker: user.id,
      skip_conflicts: skipConflicts,
    };
    api.createRecurringBooking(data)
      .then((response) => {
        let conflictsMessage = '';
        if (response.data.length > 0) {
          conflictsMessage = 'Except for:<ul>';
          // eslint-disable-next-line no-return-assign
          response.data.map(date => conflictsMessage = `${conflictsMessage}<li>${date}</li>`);
          conflictsMessage = `${conflictsMessage}</ul>`;
        }
        sweetAlert(
          'Completed',
          `Room ${selectedRoomName} was successfuly booked for the selected dates.<br/><div id="exception-dates">${conflictsMessage}</div>`,
          'success',
        )
          .then(() => {
            this.closeModalWithReservation();
          });
      })
      .catch((error) => {
        const { response } = error;

        if (response.status === 409) {
          sweetAlert({
            title: 'Reservation blocked',
            text: 'We are sorry, this reservation overlaps with other reservations. Skip reservation on already booked dates?',
            type: 'warning',
            confirmButtonText: 'YES',
            cancelButtonText: 'NO',
            showCancelButton: true,
          })
            .then((r) => {
              if (r.value) {
                this.sendPostRequestRecurringBooking(true);
              }
            });
        } else {
          sweetAlert({
            title: 'Error',
            text: response.data,
            type: 'error',
          });
        }
      });
  }

  handleSubmit = () => {
    console.log(localStorage.getItem('CapstoneReservationUser'));
    const { tabIndex, isRecurring } = this.state;
    // Verify requirements before sending the POST request
    try {
      this.verifyEndTime();
      this.verifyReservationTimes();
      if (isRecurring) {
        switch (tabIndex) {
          case 0:
            this.verifyRecurringOption0();
            break;
          default:
            throw new Error('Something went wrong');
        }
      }
    } catch (err) {
      sweetAlert('Reservation blocked', err.message, 'warning');
      return;
    }

    if (localStorage.getItem('CapstoneReservationUser') == null) {
      this.setState({ showLogin: true });
    } else if (isRecurring) {
      this.sendPostRequestRecurringBooking(false);
    } else {
      this.sendPostRequestBooking();
    }
  }

  handleCheckboxClick = () => {
    const { isRecurring } = this.state;
    this.setState({ isRecurring: !isRecurring });
  }

  handleDateChangeOption0 = (event) => {
    const { inputOption0 } = this.state;
    if (event.target.id === 'startDateOption0') {
      inputOption0.startDate = event.target.value;
    } else {
      inputOption0.endDate = event.target.value;
    }

    this.setState({
      inputOption0: {
        startDate: inputOption0.startDate,
        endDate: inputOption0.endDate,
      },
    });
  }

  renderRecurringBookingOption0 = () => {
    const { inputOption0 } = this.state;
    return (
      <div>
        <div className="modal-description">
          <h3 className="header--inline">
            <Icon name="calendar alternate" />
            {' '}
            {'Starting date'}
          </h3>
          <Form.Field>
            <Input
              size="small"
              icon="user"
              type="date"
              id="startDateOption0"
              iconPosition="left"
              value={inputOption0.startDate}
              onChange={this.handleDateChangeOption0}
            />
          </Form.Field>
        </div>
        <div className="modal-description">
          <h3 className="header--inline">
            <Icon name="calendar alternate outline" />
            {' '}
            {'End date '}
          </h3>
          <Form.Field>
            <Input
              size="small"
              icon="user"
              id="endDateOption0"
              type="date"
              value={inputOption0.endDate}
              iconPosition="left"
              onChange={this.handleDateChangeOption0}
            />
          </Form.Field>
        </div>
      </div>
    );
  }

  renderRecurringForm() {
    const panes = [
      { menuItem: 'Option 1', render: () => <Tab.Pane attached={false}>{this.renderRecurringBookingOption0()}</Tab.Pane> },
      { menuItem: 'Option 2', render: () => <Tab.Pane attached={false}>Tab 2 Content</Tab.Pane> },
      { menuItem: 'Option 3', render: () => <Tab.Pane attached={false}>Tab 3 Content</Tab.Pane> },
    ];
    return (
      <div>
        <Tab menu={{ pointing: true }} onTabChange={this.handleTabChange} panes={panes} />
      </div>
    );
  }

  renderDescription() {
    const {
      startHour,
      startMinute,
      hourOptions,
      minuteOptions,
      reservedOptions,
      isRecurring,
      endHour,
      endMinute,
    } = this.state;
    const { selectedDate } = this.props;
    return (
      <Modal.Content>
        <Modal.Description>
          <Header>
            <Icon name="calendar" />
            {selectedDate.toDateString()}
          </Header>
          <div className="modal-description">
            <h3 className="header--inline">
              <Icon className="hourglass start" />
              {'from '}
            </h3>
            <Dropdown
              selection
              compact
              placeholder="hh"
              className="dropdown--fixed-width"
              options={hourOptions}
              defaultValue={startHour}
              onChange={this.handleStartHourChange}
            />
            <Dropdown
              selection
              compact
              placeholder="mm"
              className="dropdown--fixed-width"
              options={minuteOptions}
              defaultValue={startMinute}
              onChange={this.handleStartMinuteChange}
            />
          </div>
          <div className="modal-description">
            <h3 className="header--inline">
              <Icon className="hourglass end" />
              {'to '}
            </h3>
            <Dropdown
              selection
              compact
              className="dropdown--fixed-width"
              placeholder="hh"
              options={hourOptions}
              defaultValue={endHour}
              onChange={this.handleEndHourChange}
            />
            <Dropdown
              selection
              compact
              className="dropdown--fixed-width"
              placeholder="mm"
              options={minuteOptions}
              defaultValue={endMinute}
              onChange={this.handleEndMinuteChange}
            />
          </div>
          <div className="modal-description">
            <h3 className="header--inline">
              <Icon name="user" />
              {' '}
              {'by '}
            </h3>
            <Dropdown
              selection
              compact
              className="dropdown--fixed-width"
              placeholder="hh"
              options={reservedOptions}
              defaultValue={reservedOptions[0].value}
            />

          </div>
          <div className="modal-description">
            <Checkbox label="Request a recurring booking" onClick={this.handleCheckboxClick} />
          </div>
          {isRecurring ? this.renderRecurringForm() : null}
          <div className="ui divider" />
          <div>
            <Button content="Reserve" primary onClick={this.handleSubmit} />
            <Button content="Cancel" secondary onClick={this.closeModal} />
          </div>
        </Modal.Description>
      </Modal.Content>
    );
  }

  render() {
    const { show, showLogin } = this.state;
    const { selectedRoomName } = this.props;
    return (
      <div id="reservation-details-modal">
        <Modal centered={false} size="tiny" open={show}>
          <Modal.Header>
            <Icon name="map marker alternate" />
            Room
            {selectedRoomName}
          </Modal.Header>
          {this.renderDescription()}
        </Modal>
        <Login show={showLogin} onClose={this.closeLogin} />
      </div>
    );
  }
}

ReservationDetailsModal.propTypes = {
  show: PropTypes.bool.isRequired,
  selectedRoomId: PropTypes.string.isRequired,
  selectedRoomName: PropTypes.string.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  selectedDate: PropTypes.object.isRequired,
  selectedHour: PropTypes.string.isRequired,
  minHour: PropTypes.number,
  maxHour: PropTypes.number,
  minuteInterval: PropTypes.number,
  onClose: PropTypes.func.isRequired,
  onCloseWithReservation: PropTypes.func.isRequired,
};

ReservationDetailsModal.defaultProps = {
  minHour: 8,
  maxHour: 24,
  minuteInterval: 10,
};

export default ReservationDetailsModal;
