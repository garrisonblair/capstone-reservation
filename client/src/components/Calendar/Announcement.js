import React, { Component } from 'react';
import { Message } from 'semantic-ui-react';
import moment from 'moment';
import api from '../../utils/api';
import './Calendar.scss';

class Announcement extends Component {
  state = {
    announcements: [],
    visible: true,
  }

  componentDidMount() {
    api.getAllAnnouncements()
      .then((response) => {
        this.setState({ announcements: response.data });
      });
  }

  handleDismiss = () => {
    this.setState({ visible: false });
  }

  render() {
    const { visible } = this.state;
    if (!visible) {
      return null;
    }
    const { announcements } = this.state;
    const currentDate = moment().format('YYYY-MM-DD');
    const text = [];
    announcements.forEach((a) => {
      if (moment(currentDate).isBetween(a.start_date, a.end_date)
      || moment(currentDate).isSame(a.start_date)
      || moment(currentDate).isSame(a.end_date)) {
        text.push(
          `${a.title}: ${a.content}`,
        );
      }
    });
    if (text === []) {
      return null;
    }
    return (
      <Message
        onDismiss={this.handleDismiss}
        negative
        className="announcement"
        list={text}
      />
    );
  }
}

export default Announcement;
