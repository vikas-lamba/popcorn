# -*- coding: utf-8 -*-
# Copyright (c) 2011 Ionuț Arțăriși <iartarisi@suse.cz>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from flask import abort, render_template, request

from popcorn import app
from popcorn.model import Distro, Package, System, Vendor, Submission
from popcorn.model.error import DoesNotExist
from popcorn.parse import parse_text, EarlySubmission


@app.route('/', methods=['GET'])
def index():
    distros = Distro.get_all_ids()
    vendors = Vendor.get_all_ids()
    return render_template('index.html', distros=distros, vendors=vendors)

@app.route('/', methods=['POST'])
def receive_submission():
    f = request.files['popcorn']
    try:
        parse_text(f.read())
    except (EarlySubmission, FormatError), e:
        return str(e)
    return 'Submission received. Thanks!'
    
@app.route('/vendor/<vendor_id>')
def vendor(vendor_id):
    """Return a Vendor object

    :vendor_id: the id of the Vendor

    """
    try:
        ven = Vendor.find(vendor_id)
    except DoesNotExist:
        abort(404)
    return render_template('vendor.html', vendor=ven)

@app.route('/submission/<sub_id>')
def submission(sub_id):
    """Return a Submission object"""
    try:
        sub = Submission.find(sub_id)
    except DoesNotExist:
        abort(404)
    return render_template('submission.html', submission=sub)

@app.route('/system/<hw_uuid>')
def system(hw_uuid):
    """Return a System object"""
    try:
        sys = System(hw_uuid)
    except DoesNotExist:
        abort(404)
    return render_template('system.html', system=sys)

@app.route('/package/<pkg_id>')
def package(pkg_id):
    """Return a Package object"""
    try:
        pkg = Package.find(pkg_id)
    except DoesNotExist:
        abort(404)
    return render_template('package.html', package=pkg)

@app.route('/distro/<distro_id>')
def distro(distro_id):
    """Return a Distro object"""
    try:
        dist = Distro.find(distro_id)
    except DoesNotExist:
        abort(404)
    return render_template('distro.html', distro=dist)