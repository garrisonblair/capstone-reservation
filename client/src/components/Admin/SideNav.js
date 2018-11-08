import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import './SideNav.scss';


class SideNav extends Component {

  goToSettings = () => {
    this.props.history.push('/admin/settings')
  }

  goToStats = () => {
    this.props.history.push('/admin/stats')
  }

  render() {
    const {selectedMenu} = this.props;
    return (
      <div className="admin-nav">
        <ul>
          <li
            className={selectedMenu === 'settings'? 'active': ''}
            onClick={this.goToSettings}
          >
            Settings
          </li>
          <li
            className={selectedMenu === 'stats'? 'active': ''}
            onClick={this.goToStats}
          >
            Stats
          </li>
        </ul>
      </div>
    )
  }
}

export default withRouter(SideNav);
