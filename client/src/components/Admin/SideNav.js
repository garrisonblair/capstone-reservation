import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import './SideNav.scss';


class SideNav extends Component {

  render() {
    const {selectedMenu} = this.props;
    return (
      <div className="admin-nav">
        <ul>
          <li
            className={selectedMenu === 'settings'? 'active': ''}
          >
            <Link
              to={'settings'}
            >
              Settings
            </Link>
          </li>
          <li
            className={selectedMenu === 'stats'? 'active': ''}
          >
            <Link
              to={'stats'}
            >
              Stats
            </Link>
          </li>
        </ul>
      </div>
    )
  }
}

export default SideNav;
