from flask import Blueprint, render_template_string, request
import sqlite3
import pandas as pd
import plotly.express as px
import random
import config