/* eslint-disable no-console */
import React, { Component } from 'react';
import AdminRequired from '../../HOC/AdminRequired';
import RoomStats from './RoomStats';
import api from '../../../utils/api';
import '../Admin.scss';


// eslint-disable-next-line react/prefer-stateless-function
class Stats extends Component {
  state = {
    roomStats: [],
  }

  componentDidMount() {
    api.getRoomStatistics()
      .then((response) => {
        const { data: roomStats } = response;
        this.setState({ roomStats });
      });
  }

  render() {
    const { roomStats } = this.state;
    return (
      <div className="stats">
        <RoomStats stats={roomStats} />
      </div>
    );
  }
}

export default AdminRequired(Stats);
