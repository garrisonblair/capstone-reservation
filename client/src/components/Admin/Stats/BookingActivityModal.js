import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Header, Icon, Modal,
} from 'semantic-ui-react';

class BookingActivityModal extends Component {
  static formatDate(d) {
    const date = d.split('T');
    const time = date[1].split('.');
    return `${date[0]}\n${time[0]}`;
  }

  static formatAction(flag) {
    if (flag === 1) {
      return 'Create';
    }
    if (flag === 2) {
      return 'Edit';
    }
    if (flag === 3) {
      return 'Delete';
    }
    return '';
  }

  renderBoolean = boolean => (
    <Icon
      name={boolean ? 'check circle' : 'times circle'}
      color={boolean ? 'green' : 'red'}
    />
  )

  render() {
    const { show, onClose, log } = this.props;
    if (log != null) {
      const obj = JSON.parse(log.object_repr);
      return (
        <Modal className="booking-activity-modal" open={show} onClose={onClose}>
          <Header>
            Details
          </Header>
          <div>
            <table>
              <tbody>
                <tr>
                  <th>Date</th>
                  <td>{BookingActivityModal.formatDate(log.action_time)}</td>
                </tr>
                <tr>
                  <th>Action</th>
                  <td>
                    {BookingActivityModal.formatAction(log.action_flag)}
                    &nbsp;{log.content_type.model}
                  </td>
                </tr>
                <tr>
                  <th>User</th>
                  <td>{log.user.username}</td>
                </tr>
              </tbody>
            </table>
            <br />
            <table>
              <tbody>
                <tr>
                  <th>ID</th>
                  <td>{obj.id}</td>
                </tr>
                <tr>
                  <th>{obj.date ? 'Date' : 'End Date'}</th>
                  <td>{obj.date ? obj.date : obj.end_date}</td>
                </tr>
                <tr>
                  <th>Start Time</th>
                  <td>{obj.start_time ? obj.start_time : obj.booking_start_time}</td>
                </tr>
                <tr>
                  <th>End Time</th>
                  <td>{obj.end_time ? obj.end_time : obj.booking_end_time}</td>
                </tr>
                <tr>
                  <th>Room</th>
                  <td>{obj.room}</td>
                </tr>
                <tr>
                  <th>Booker</th>
                  <td>{obj.booker}</td>
                </tr>
                <tr>
                  <th>Group</th>
                  <td>{obj.group == null ? 'None' : obj.group}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="ui divider" />
          <div className="controls">
            <Button icon labelPosition="left" negative size="small" onClick={onClose}>
              <Icon name="x" />
              Close
            </Button>
          </div>
        </Modal>
      );
    }
    return null;
  }
}

BookingActivityModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  log: PropTypes.instanceOf(Object),
};

BookingActivityModal.defaultProps = {
  log: null,
};

export default BookingActivityModal;